import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FanForm({ onSubmit }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [cpf, setCpf] = useState('');
  const [address, setAddress] = useState('');
  const [activities, setActivities] = useState('');
  const [twitter, setTwitter] = useState(''); 
  const [interests, setInterests] = useState({
    'CS:GO': false,
    'FURIA': false,
    'Eventos presenciais': false,
  });
  const [file, setFile] = useState(null);

  const toggleInterest = key =>
    setInterests(prev => ({ ...prev, [key]: !prev[key] }));

  const onDrop = useCallback(acceptedFiles => {
    setFile(acceptedFiles[0]);
  }, []);
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/*': [] },
    multiple: false,
  });

  const handleSubmit = e => {
    e.preventDefault();
    const cleanedCpf = cpf.replace(/\D/g, '');
    const cpfRegex = /^\d{11}$/;
    if (!cpfRegex.test(cleanedCpf)) {
      alert('Por favor, insira um CPF válido com 11 dígitos.');
      return;
    }
    const payload = {
      name,
      email,
      cpf: cleanedCpf,
      address,
      activities,
      interests: Object.keys(interests).filter(i => interests[i]),
      twitter,
      file,
    };
    onSubmit(payload);
  };

  return (
    <div className="form-with-logos">
      <img
        src="/src/assets/furia-logo.png"
        alt="FURIA Logo"
        className="side-logo left"
      />
      <form onSubmit={handleSubmit} className="form-container">
        <div className="form-group">
          <label>Nome completo</label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>E-mail</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>CPF</label>
          <input
            type="text"
            value={cpf}
            onChange={e => {
              const digits = e.target.value.replace(/\D/g, '').slice(0, 11);
              const withMask = digits
                .replace(/^(\d{3})(\d)/, '$1.$2')
                .replace(/^(\d{3}\.\d{3})(\d)/, '$1.$2')
                .replace(/^(\d{3}\.\d{3}\.\d{3})(\d)/, '$1-$2');
              setCpf(withMask);
            }}
            placeholder="000.000.000-00"
            title="Formato: 000.000.000-00"
            required
          />
        </div>

        <div className="form-group">
          <label>Endereço</label>
          <input
            type="text"
            value={address}
            onChange={e => setAddress(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>Twitter</label>
          <input
            type="text"
            placeholder="@seu_handle"
            value={twitter}
            onChange={e => setTwitter(e.target.value)}
          />
        </div>

        <fieldset className="form-group checkbox-group">
          <legend>Interesses</legend>
          {Object.keys(interests).map(key => (
            <label key={key}>
              <input
                type="checkbox"
                checked={interests[key]}
                onChange={() => toggleInterest(key)}
              />
              {key}
            </label>
          ))}
        </fieldset>

        <div className="form-group activities-group">
          <label>Atividades/Eventos/Compras</label>
          <textarea
            className="activities-textarea"
            value={activities}
            onChange={e => setActivities(e.target.value)}
            rows={5}
            required
          />
        </div>

        <div className="side-by-side-container">
          <div className="dropzone-container">
            <div {...getRootProps()} className="dropzone">
              <input {...getInputProps()} />
              {isDragActive ? (
                <p>Solte a imagem do documento aqui…</p>
              ) : (
                <p>Arraste a foto do seu RG/CPF ou clique para selecionar</p>
              )}
              {file && <p>✓ {file.name}</p>}
            </div>
          </div>
        </div>

        <button type="submit">Enviar</button>
      </form>
    </div>
  );
}
