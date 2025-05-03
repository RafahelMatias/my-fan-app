import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';

export default function FanForm({ onSubmit }) {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [cpf, setCpf] = useState('');
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

    const cpfRegex = /^\d{11}$/; // Apenas 11 dígitos
    if (!cpfRegex.test(cleanedCpf)) {
      alert('Por favor, insira um CPF válido com 11 dígitos.');
      return;
    }

    const payload = {
      name,
      email,
      cpf: cleanedCpf, 
      interests: Object.keys(interests).filter(i => interests[i]),
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
          <label >Nome completo </label>
          <input
            type="text"
            value={name}
            onChange={e => setName(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>E-mail </label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="form-group">
          <label>CPF </label>
          <input
            type="text"
            value={cpf}
            onChange={e => {
              // pega só dígitos e limita a 11 chars
              const digits = e.target.value.replace(/\D/g, '').slice(0, 11);
              // insere pontos e hífen conforme vamos tendo dígitos
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
