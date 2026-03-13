const express = require("express")
const multer = require("multer")
const cors = require("cors")
const { exec } = require("child_process")
const path = require("path")

const app = express()
app.use(cors())

const storage = multer.diskStorage({
  destination: "uploads/",
  filename: (req, file, cb) => {
    cb(null, Date.now() + path.extname(file.originalname))
  }
})

const upload = multer({
  storage: storage,
  limits: { fileSize: 10 * 1024 * 1024 * 1024 }
})

app.post("/upload", upload.single("video"), (req, res) => {

  const videoPath = req.file.path

  const command = `python ../worker/process_video.py ${videoPath}`

  exec(command, (error, stdout, stderr) => {

    if (error) {
      console.log(error)
      return res.status(500).send("Processing failed")
    }

    res.json({
      message: "Processing complete",
      output: stdout
    })
  })
})

app.use("/output", express.static("../outputs"))

app.listen(3000, () => {
  console.log("Server running on port 3000")
})
