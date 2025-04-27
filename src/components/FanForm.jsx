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

    // Remove quaisquer caracteres extras do CPF antes de validar
    const cleanedCpf = cpf.replace(/\D/g, '');

    // Validação explícita do CPF
    const cpfRegex = /^\d{11}$/; // Apenas 11 dígitos
    if (!cpfRegex.test(cleanedCpf)) {
      alert('Por favor, insira um CPF válido com 11 dígitos.');
      return;
    }

    const payload = {
      name,
      email,
      cpf: cleanedCpf, // Envia o CPF limpo
      interests: Object.keys(interests).filter(i => interests[i]),
      file,
    };
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} style={{ maxWidth: 400, margin: '0 auto' }}>
      <div>
        <label>Nome completo</label>
        <input
          type="text"
          value={name}
          onChange={e => setName(e.target.value)}
          required
        />
      </div>

      <div>
        <label>E-mail</label>
        <input
          type="email"
          value={email}
          onChange={e => setEmail(e.target.value)}
          required
        />
      </div>

      <div>
        <label>CPF</label>
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

      <fieldset style={{ margin: '1em 0' }}>
        <legend>Interesses</legend>
        {Object.keys(interests).map(key => (
          <label key={key} style={{ display: 'block' }}>
            <input
              type="checkbox"
              checked={interests[key]}
              onChange={() => toggleInterest(key)}
            />{' '}
            {key}
          </label>
        ))}
      </fieldset>

      <div
        {...getRootProps()}
        style={{
          border: '2px dashed #888',
          padding: 20,
          textAlign: 'center',
          marginBottom: 16,
        }}
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <p>Solte a imagem do documento aqui…</p>
        ) : (
          <p>Arraste a foto do seu RG/CPF ou clique para selecionar</p>
        )}
        {file && <p>✓ {file.name}</p>}
      </div>

      <button type="submit">Enviar</button>
    </form>
  );
}
