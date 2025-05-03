import FanForm from './components/FanForm';

function App() {
  const handleFormSubmit = async (data) => {
    const formData = new FormData();
    formData.append('name', data.name);
    formData.append('email', data.email);
    formData.append('cpf', data.cpf);
    formData.append('address', data.address);
    formData.append('activities', data.activities);
    formData.append('interests', JSON.stringify(data.interests));
    formData.append('twitter', data.twitter);
    formData.append('file', data.file);

    try {
      const res = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        body: formData
      });
      const json = await res.json();
      if (!res.ok) throw new Error(json.error || json.detail || 'Falha no envio');
      alert(json.message || 'Dados enviados!');
    } catch (error) {
      alert('Erro de conexão com o servidor. Verifique se o backend está rodando em http://localhost:8000');
      console.error(error);
    }
  };

  return (
    <div>
      <h1>Know Your Fan</h1>
      <FanForm onSubmit={handleFormSubmit} />
    </div>
  );
}

export default App;
