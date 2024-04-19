1. in this repo mainly for poc purpose
2. Extract data from image like aadhar, pan, driving, voter id.
3. and convert data into json object.
   setuping the project.
   1. this is python based poc.
   2. pip install opencv-python-headless pytesseract base64.
   3. run the project.
   4. its runs in port number 5000
   5. use postman and create post request
   6.  in endpoint is /extract-data
   7.  body { doc_type: 'aadhar', image: //here add image base64 url }
     

      
