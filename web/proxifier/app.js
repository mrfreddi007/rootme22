const parseUrl = require("parse-url");
const urlParse = require("url-parse");
const fetch = require("node-fetch");
const express = require("express");
const path = require("path");
const fs = require("fs");


const FLAG_PATH = "*sensored*";
const app = express();


var getURL = async (url) => {
  // INIT
  var protocol = urlParse(url)["protocol"];
  var host = urlParse(url)["host"];
  var pathname = urlParse(url)["pathname"];

  if (protocol === "https:" && host.endsWith("root-me.org")) {
    // DOUBLE CHECK
    protocol = parseUrl(url)["protocol"];
    host = new URL(pathname, `https://root-me.org/mizu`)["host"];
    pathname = new URL(pathname, `https://root-me.org/mizu`)["pathname"];

    // REMOTE
    if (protocol === "https") {
      try {
        var res = await fetch(`${protocol}://${host}${pathname}`);
        res = await res.text();
        return res
      } catch {
        return "Error fetching data.";
      }

      // LOCAL
    } else if (protocol === "file" && host === "127.0.0.1") {
      try {
        return fs.readFileSync(pathname, "utf8");
      } catch {
        return "No such file or directory.";
      }
    }

  } else {
    return "Protocol must be https and host end with 'root-me.org'.";
  }
}


app.get("/proxy", async (req, res) => {
  if (req.query.url !== undefined) {
    res.send(await getURL(req.query.url));
  } else {
    res.send("[ERROR] No URL send!")
  }
});


app.listen(3000, () => {
  console.log(`Express server listening on port 3000`)
})
