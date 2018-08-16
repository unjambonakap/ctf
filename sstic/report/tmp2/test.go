package tar

import (
  "bytes"
  "fmt"
  "io"
  "io/ioutil"
  "log"
  "reflect"
)

import "encoding/json"

func check(e error) {
  if e != nil {
    panic(e)
  }
}

type Test1 struct {
  Data   []byte
  Offset int64
}

func Example() {
  // Create a buffer to write our archive to.
  dat, err := ioutil.ReadFile("./huge.tar")
  check(err)
  fmt.Print("Contents of %d\n", len(dat))

  // Open the tar archive for reading.
  r := bytes.NewReader(dat)
  tr := NewReader(r)

  // Iterate through the files in the archive.
  var entries []Test1
  for {
    hdr, err := tr.Next()
    if err == io.EOF {
      // end of tar archive
      break
    }
    if err != nil {
      log.Fatalln(err)
    }
    fmt.Println(reflect.TypeOf(hdr))
    fmt.Println(tr.curr)
    entry := tr.curr.(*sparseFileReader)

    for index, elem1 := range entry.sp {
      var s = make([]byte, elem1.numBytes)
      n, err := entry.rfr.Read(s)
      fmt.Printf("Got sp entry of idx=%d %s: %d %s >> %s\n", 
      index, elem1, n, err, s)
      entries = append(entries, Test1{Data: s, Offset: elem1.offset})
    }
    res, _ := json.Marshal(entries)
    err = ioutil.WriteFile("/tmp/dat1", res, 0644)
    check(err)
    fmt.Println()
  }
}
