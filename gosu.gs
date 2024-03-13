uses java.io.BufferedReader
uses java.io.InputStreamReader
uses java.io.OutputStreamWriter
uses java.net.HttpURLConnection
uses java.net.URL
uses java.net.URLEncoder

//var data = "Tell me something about guidewire workers compensation"
var data = "How is the weather in Dehradun, Uttarakhand, India"
var output = sendDataToPythonApi(data)
if (output != null) {
  print(output)
}

  function sendDataToPythonApi(prompt : String) : String {
    var apiUrl = "http://localhost:5000/api/auth"
    var url = new URL(apiUrl)
    var con = url.openConnection() as HttpURLConnection
    con.RequestMethod = "POST"
    con.setRequestProperty("Content-Type", "application/json")
    con.setRequestProperty("Authorization", "")
    con.DoOutput = true

    var payload = "{\n  \"prompt\": \"" + URLEncoder.encode(prompt, "UTF-8") + "\"\n}"
    var writer = new OutputStreamWriter(con.OutputStream)
    writer.write(payload)
    writer.flush()

    var responseCode = con.ResponseCode
    if (responseCode == HttpURLConnection.HTTP_OK) {
      var inputStream = con.InputStream
      var reader = new BufferedReader(new InputStreamReader(inputStream))
      var response = new StringBuilder()
      var line = reader.readLine()
      while (line != null) {
        response.append(line)
        line = reader.readLine()
      }
      reader.close()
      var cleanedResponse = response.toString().replace("\\n", "\n").replace("\\*\\*", "**")
      return cleanedResponse
    } else {
      print("POST request failed. Response code: " + responseCode)
      return null
    }
  }