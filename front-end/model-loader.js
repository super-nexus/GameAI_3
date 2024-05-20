const modelSelect = document.querySelector('.model-select'),
  llmLoading = document.querySelector('.llm-loading');



modelSelect.addEventListener('change', async () => {
  const model = modelSelect.value;


  llmLoading.style.display = 'flex';
  await fetch(`/agent`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ agent : model })
  })
  .then(async (data) => await data.json())
  .then((data) => {
    console.log(data);
  })
  .catch((err) => {
    console.log(err);
  });

  llmLoading.style.display = 'none';
});


fetch(`/agent`)
.then(async (data) => await data.json())
.then((data) => {
  modelSelect.value = data.agent;
})
.catch((err) => {
  console.log(err);
});