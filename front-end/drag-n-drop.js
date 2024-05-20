const dropArea = document.querySelector(".drag-image"),
dragText = dropArea.querySelector("h6"),
button = dropArea.querySelector(".browse-file-btn"),
input = dropArea.querySelector(".file-input"),
deleteButton = dropArea.querySelector(".delete-file-btn"),
submitBtn = document.querySelector(".submit-form .submit-btn");

let file; 

button.onclick = ()=>{
  input.click(); 
}

input.addEventListener("change", function(){
  file = this.files[0];
  dropArea.classList.add("active");
  viewfile();
});

dropArea.addEventListener("dragover", (event)=>{
  event.preventDefault();
  dropArea.classList.add("active");
  dragText.textContent = "Release to Upload File";
});


dropArea.addEventListener("dragleave", ()=>{
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
}); 

dropArea.addEventListener("drop", (event)=>{
  event.preventDefault(); 
   
  file = event.dataTransfer.files[0];
  viewfile(); 
});

deleteButton.onclick = ()=>{
  resetFileInput();
}

function viewfile(){
  let fileType = file.type; 
  let validExtensions = ["image/jpeg", "image/jpg", "image/png"];
  if(validExtensions.includes(fileType)){ 
    let fileReader = new FileReader(); 
    fileReader.onload = ()=>{
      let fileURL = fileReader.result; 
      let imgTag = `<img src="${fileURL}" alt="image">`;
      dropArea.innerHTML = imgTag; 
      dropArea.appendChild(deleteButton);
      deleteButton.hidden = false;
    }
    fileReader.readAsDataURL(file);
    submitBtn.disabled = false;
  }else{
    alert("This is not an Image File!");
    dropArea.classList.remove("active");
    dragText.textContent = "Drag & Drop to Upload File";
  }
}


function resetFileInput() {
  file = null;
  input.value = "";
  dropArea.classList.remove("active");
  dragText.textContent = "Drag & Drop to Upload File";
  dropArea.innerHTML = `
    <h6>Drag & Drop File Here</h6>
    <span>OR</span>
    <button class="browse-file-btn" type="button">Browse File</button>
    <input class="file-input" type="file" hidden>
  `;
  dropArea.querySelector(".browse-file-btn").onclick = () => input.click();
  deleteButton.hidden = true;
  submitBtn.disabled = true;

  responseWrapper.style.display = "none";
  responseBox.textContent = "";
  regionBox.textContent = "";
  countryBox.textContent = "";
}