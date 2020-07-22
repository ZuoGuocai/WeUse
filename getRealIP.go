package main

import (
    "fmt"
    "io"
    "log"
    "net/http"
    "net/http/httputil"
)

func main() {
    log.Println("Server hello-world")
    http.HandleFunc("/", AppRouter)
    http.ListenAndServe(":12345", nil)
}

func AppRouter(w http.ResponseWriter, r *http.Request) {
    dump, _ := httputil.DumpRequest(r, false)
    log.Printf("%q\n", dump)
    io.WriteString(w, fmt.Sprintf("Guest come from %v\n", r.RemoteAddr))
    return
}
