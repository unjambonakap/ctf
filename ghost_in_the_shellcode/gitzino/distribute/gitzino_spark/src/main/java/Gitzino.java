import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.fs.Path;
import org.apache.spark.SparkConf;
import org.apache.spark.api.java.JavaPairRDD;
import org.apache.spark.api.java.JavaRDD;
import org.apache.spark.api.java.JavaSparkContext;
import org.apache.spark.serializer.KryoRegistrator;

import com.esotericsoftware.kryo.Kryo;
import com.esotericsoftware.kryo.serializers.FieldSerializer;

import scala.Tuple2;

public class Gitzino {
    public static final int NUM_HAND_CARDS = 5;
    public static final int NUM_DECK_CARDS = 52;
    public static final String PERM_FILE = "permutations.out";

    public static class Hand {

        public Hand(int hand) {
            int cur = hand;
            for (int i = 0; i < NUM_HAND_CARDS; ++i) {
                cards[i] = cur & 0x3f;
                cur >>= 6;
            }
        }

        public int[] cards = new int[NUM_HAND_CARDS];
    }


    public static class Permutation {
        public int low, high, seed;

        public static int fromCards(int[] tb, int offset) {
            int tmp = 0;
            for (int i = NUM_HAND_CARDS - 1; i >= 0; --i)
                tmp = (tmp << 6) | tb[offset + i];
            return tmp;

        }

        public static Permutation fromSeed(int seed) {
            Permutation res = new Permutation();
            MersenneTwisterFast rng = new MersenneTwisterFast(seed);
            int[] tb = new int[NUM_DECK_CARDS];
            for (int i = 0; i < tb.length; ++i)
                tb[i] = i;

            for (int i = tb.length - 1; i >= 0; --i) {
                int x = rng.nextInt() % (i + 1);
                if (x < 0)
                    x += i + 1;
                int c = tb[i];
                tb[i] = tb[x];
                tb[x] = c;
            }

            res.seed = seed;
            res.low = fromCards(tb, 0);
            res.high = fromCards(tb, NUM_HAND_CARDS);
            return res;
        }

    }

    public static class OpaRegistrator implements KryoRegistrator {

        @Override
        public void registerClasses(Kryo kryo) {
            System.out.println("KAPAPA");
            kryo.register(Permutation.class, new FieldSerializer<>(kryo, Permutation.class));
        }
    }


    public static Tuple2<Integer, Permutation> computePermutation(long seed) {
        Permutation res = Permutation.fromSeed((int) seed);
        return new Tuple2<Integer, Gitzino.Permutation>(res.low, res);
    }

    public static void main(String[] args) {

        SparkConf conf = new SparkConf().setAppName("Gitzino");
        conf.set("spark.serializer", "org.apache.spark.serializer.KryoSerializer");
        conf.registerKryoClasses(new Class<?>[] {Permutation.class});
        // conf.set("spark.kryo.registrator", "Gitzino.OpaRegistrator");
        JavaSparkContext sc = new JavaSparkContext(conf);

        try {
            FileSystem fs =
                    FileSystem.get(new java.net.URI("file:///home/spark/prog/gitzino_spark"),
                            new Configuration());
            fs.delete(new Path(PERM_FILE), true);

            long tot = 1l << 32;
            long batchSize = 1 << 20;
            long nblocks = tot / batchSize;

            JavaRDD<Long> last = null;
            for (int i = 0; i < nblocks; ++i) {
                ArrayList<Long> lst = new ArrayList<>();
                long val = batchSize * i;
                for (int j = 0; j < batchSize; ++j)
                    lst.add(i + val);


                JavaRDD<Long> cur = sc.parallelize(lst, 1 << 5);
                if (last == null)
                    last = cur;
                else
                    last = last.union(cur);
            }

            last.mapToPair(x -> computePermutation(x)).groupByKey().saveAsTextFile(PERM_FILE);

        } catch (IOException | URISyntaxException e) {
            System.out.println("Got exception >> " + e.getMessage());
            e.printStackTrace();
        }

    }
}
