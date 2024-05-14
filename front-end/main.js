const submitForm = document.querySelector('.submit-form');
const responseWrapper = document.querySelector('.response-wrapper'),
  responseBox = responseWrapper.querySelector('.llm-response'),
  countryBox = responseWrapper.querySelector('.llm-response-country'),
  regionBox = responseWrapper.querySelector('.llm-response-region'),
  loader = submitForm.querySelector('.loader');



submitForm.addEventListener('submit', async (e) => {
  e.preventDefault();

  if (!file) {
    alert('Please select an image to upload');
    return;
  }

  const formData = new FormData();
  formData.append('image', file);

  loader.style.display = 'block';

  await fetch('/upload', {
    method: 'POST',
    body: formData
  }).then(async (data) => await data.json())
  .then((data) => {
    responseWrapper.style.display = 'block';
    console.log(data);
    responseBox.textContent = data.message.image_description;
    regionBox.textContent = data.message.region;
    countryBox.textContent = data.message.country;
  })
  .catch((err) => {
    console.log(err);
    //delete this after backend is working.
    //this is only for demo purposes
    responseWrapper.style.display = 'block';
    responseBox.textContent = "This appers to be in the country of France. Somewhere in the southern region."
  }).finally(() => {
    loader.style.display = 'none';
  });
});
