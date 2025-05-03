import { useState } from 'react';
import FanForm from './components/FanForm';

function App() {
  const [twitterData, setTwitterData] = useState(null);

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
      
      // Fetch Twitter data if handle provided
      if (data.twitter) {
        const handle = data.twitter.replace('@', '');
        const twResp = await fetch(`http://localhost:8000/twitter/${handle}`);
        const twJson = await twResp.json();
        setTwitterData(twJson);
      }

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
      
      {twitterData && (
        <div className="twitter-info">
          <h2>{twitterData.profile.name}</h2>
          <p>Seguidores: {twitterData.profile.public_metrics.followers_count}</p>
          <h3>Últimos tweets:</h3>
          <ul>
            {twitterData.recent_tweets.map((tweet, i) => (
              <li key={i}>{tweet}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default App;
