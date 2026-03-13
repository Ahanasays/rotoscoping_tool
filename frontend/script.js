async function uploadVideo() {

  const file = document.getElementById("videoFile").files[0]

  const formData = new FormData()
  formData.append("video", file)

  document.getElementById("status").innerText = "Uploading..."

  const response = await fetch("http://localhost:3000/upload", {
    method: "POST",
    body: formData
  })

  const data = await response.json()

  document.getElementById("status").innerText =
    "Processing complete!"
}
