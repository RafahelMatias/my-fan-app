import FanForm from './components/FanForm';

function App() {
  const handleFormSubmit = async (data) => {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('email', data.email);
    formData.append('cpf', data.cpf);
    formData.append('interests', JSON.stringify(data.interests));
    formData.append('file', data.file);

    // envia para o backend FastAPI
    const res = await fetch('https://<seu-backend>/submit', {
      method: 'POST',
      body: formData,
    });
    if (res.ok) alert('Dados enviados!');
    else alert('Falha no envio.');
  };

  return (
    <div>
      <h1>Know Your Fan</h1>
      <FanForm onSubmit={handleFormSubmit} />
    </div>
  );
}

export default App;
