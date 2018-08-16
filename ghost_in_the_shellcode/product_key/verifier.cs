using System;


public class ProductKeyVerifier {
    public static int Main(string [] args){
        int serialNumber;
        string s=args[0];
        bool res=ProductKeyVerifier.VerifyKey(s,  ProductType.SeasonPass, out serialNumber);
        Console.WriteLine("Output for {0} >> ok={1} serial={2}", s, res, serialNumber);
        return 0;
    }


    public enum ProductType
    {
        SeasonPass = 1
    }
    private const string validChars = "12346789ABCDEFGHIJKLMNPQRTUVWXYZ";
    private static int[] A = new int[]
    {
        271135,
            185705,
            872007,
            1022754,
            413042
    };
    private static int[] B = new int[]
    {
        821273,
            66000,
            7662,
            386178,
            611981
    };
    private static int[] C = new int[]
    {
        770098,
            621577,
            992113,
            830442,
            243815
    };
    private static int[] D = new int[]
    {
        376235,
            84434,
            1019539,
            784643,
            594329
    };
    private static int[] E = new int[]
    {
        284649,
            885640,
            213732,
            236091,
            132494
    };
    private static int[] F = new int[]
    {
        615228,
            967387,
            708052,
            69554,
            150828
    };
    private static int[] G = new int[]
    {
        318496,
            486875,
            327057,
            320030,
            560587
    };
    private static int[] shiftA = new int[]
    {
        5,
            7,
            11,
            13,
            17
    };
    private static int[] shiftB = new int[]
    {
        3,
            6,
            9,
            12,
            15
    };
    private static int[] shiftC = new int[]
    {
        16,
            11,
            8,
            4,
            2
    };
    private static int CharToValue(char ch)
    {
        for (int i = 0; i < "12346789ABCDEFGHIJKLMNPQRTUVWXYZ".Length; i++)
        {
            if ("12346789ABCDEFGHIJKLMNPQRTUVWXYZ"[i] == ch)
            {
                return i;
            }
        }
        return -1;
    }
    private static int Rol(int val, int shift)
    {
        return (val << shift & 1048575) | val >> 20 - shift;
    }
    public static bool VerifyKey(string key, ProductKeyVerifier.ProductType type, out int serialNumber)
    {
        serialNumber = 0;
        string text = "";
        for (int i = 0; i < key.Length; i++)
        {
            if (key[i] != ' ' && key[i] != '-')
            {
                text += char.ToUpper(key[i]);
            }
        }
        if (text.Length != 25)
        {
            return false;
        }
        string[] array = new string[5];
        for (int j = 0; j < 5; j++)
        {
            array[j] = text.Substring(5 * j, 5);
            for (int k = 0; k < 5; k++)
            {
                if (ProductKeyVerifier.CharToValue(array[j][k]) == -1)
                {
                    return false;
                }
            }
            int num = 0;
            for (int l = 0; l < 4; l++)
            {
                num += ProductKeyVerifier.CharToValue(array[j][l]);
            }
            if (array[j][4] != "12346789ABCDEFGHIJKLMNPQRTUVWXYZ"[num % 32])
            {
                return false;
            }
            Console.WriteLine("HERE {0} {1}", num%32, array[j][4]);
            array[j] = array[j].Substring(0, 4);
        }
        int[] array2 = new int[5];
        for (int m = 0; m < 5; m++)
        {
            int num2 = 0;
            for (int n = 0; n < 4; n++)
            {
                num2 *= 32;
                num2 += ProductKeyVerifier.CharToValue(array[m][n]);
            }
            array2[m] = num2;
        }
        for (int num3 = 0; num3 < 5; num3++)
        {
            array2[num3] = (ProductKeyVerifier.Rol(array2[num3] ^ ProductKeyVerifier.A[num3], ProductKeyVerifier.shiftA[num3]) - ProductKeyVerifier.Rol(array2[num3] ^ ProductKeyVerifier.B[num3], ProductKeyVerifier.shiftB[num3]) & 1048575);
        }
        int[] array3 = new int[5];
        for (int num4 = 0; num4 < 5; num4++)
        {
            Console.WriteLine("got "+array2[num4]);
            array3[num4] = (ProductKeyVerifier.Rol(array2[num4] ^ ProductKeyVerifier.C[num4], ProductKeyVerifier.shiftC[0]) + ProductKeyVerifier.Rol(array2[(num4 + 1) % 5] ^ ProductKeyVerifier.D[num4], ProductKeyVerifier.shiftC[1]) + ProductKeyVerifier.Rol(array2[(num4 + 2) % 5] ^ ProductKeyVerifier.E[num4], ProductKeyVerifier.shiftC[2]) + ProductKeyVerifier.Rol(array2[(num4 + 3) % 5] ^ ProductKeyVerifier.F[num4], ProductKeyVerifier.shiftC[3]) + ProductKeyVerifier.Rol(array2[(num4 + 4) % 5] ^ ProductKeyVerifier.G[num4], ProductKeyVerifier.shiftC[4]) & 1048575);
            Console.WriteLine("for {0} got {1}", num4, array3[num4]);
        }
        serialNumber = ((array3[0] & 4095) << 20 | array3[1]);
        int num5 = array3[0] >> 12 & 255;
        return num5 == (int)type && array3[2] == 0 && array3[3] == 0 && array3[4] == 0;
    }
}
