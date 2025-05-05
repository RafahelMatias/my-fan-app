/*
  Este arquivo representa o componente principal do aplicativo "Know Your Fan".
  Ele gerencia o estado dos dados vindos do backend, envia formulários e exibe:
    - Dados do Twitter para o usuário e tweets recentes relacionados ao #FURIA.
    - O formulário de entrada de dados dos fãs.
  A lógica de requisições e tratamento de erros está implementada em handleFormSubmit.
*/

import { useState } from 'react'
import FanForm from './components/FanForm'

function App() {
  const [twitterData, setTwitterData] = useState(null)
  const [furiaTweets, setFuriaTweets] = useState([])

  const handleFormSubmit = async (data) => {
    // Limpa o estado anterior e monta os dados a enviar
    setTwitterData(null)
    setFuriaTweets([])

    const formData = new FormData()
    formData.append('name', data.name)
    formData.append('email', data.email)
    formData.append('cpf', data.cpf)
    formData.append('address', data.address)
    formData.append('activities', data.activities)
    formData.append('interests', JSON.stringify(data.interests))
    formData.append('twitter', data.twitter)
    formData.append('file', data.file)

    try {
      const res = await fetch('http://localhost:8000/submit', {
        method: 'POST',
        body: formData,
      })
      const json = await res.json()
      if (!res.ok) throw new Error(json.error || json.detail || 'Falha no envio')

      if (data.twitter) {
        try {
          const handle = data.twitter.replace(/^@/, '')
          const twResp = await fetch(`http://localhost:8000/twitter/${handle}`)
          const twJson = await twResp.json()
          
          if (!twResp.ok) throw new Error(twJson.detail || 'Falha ao buscar dados do Twitter')
          setTwitterData(twJson)
        } catch (twitterError) {
          console.error('Error fetching Twitter data:', twitterError)
          setTwitterData({
            profile: { name: data.twitter, public_metrics: { followers_count: 'N/A' } },
            recent_tweets: ['Erro ao carregar tweets. Tente novamente mais tarde.']
          })
        }
      }

      // busca os tweets em destaque do #FURIA
      try {
        const furiaResp = await fetch('http://localhost:8000/twitter/furia')
        const furiaJson = await furiaResp.json()
        
        if (!furiaResp.ok) throw new Error(furiaJson.detail || 'Falha ao buscar tweets da FURIA')
        setFuriaTweets(furiaJson.recent_tweets || [])
      } catch (furiaError) {
        console.error('Error fetching FURIA tweets:', furiaError)
        setFuriaTweets(['Erro ao carregar tweets da FURIA. Tente novamente mais tarde.'])
      }

      alert(json.message || 'Dados enviados!')
    } catch (error) {
      // Tratamento de erro de conexão com o backend
      alert(
        'Erro de conexão com o servidor. Verifique se o backend está rodando em http://localhost:8000'
      )
      console.error(error)
    }
  }

  return (
    <div>
      <h1>Know Your Fan</h1>
      <FanForm onSubmit={handleFormSubmit} />
      {/* Exibe informações do Twitter caso existam */}
      {twitterData && twitterData.recent_tweets.length > 0 && (
        <div className="twitter-info">
          <h2>{twitterData.profile.name}</h2>
          <p>Seguidores: {twitterData.profile.public_metrics.followers_count || 'N/A'}</p>
          <h3>Últimos tweets:</h3>
          <ul>
            {twitterData.recent_tweets.map((tweet, i) => (
              <li key={i}>{tweet}</li>
            ))}
          </ul>
        </div>
      )}
      {/* Exibe tweets em destaque do #FURIA */}
      {furiaTweets.length > 0 && (
        <section style={{ marginTop: '2rem', textAlign: 'left' }}>
          <h2>Em destaque do #FURIA</h2>
          <ul>
            {furiaTweets.map((t, i) => (
              <li key={i}>{t}</li>
            ))}
          </ul>
        </section>
      )}
    </div>
  )
}

export default App
