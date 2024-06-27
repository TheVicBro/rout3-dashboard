import { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../context/authContext';

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const router = useRouter();

  const handleLogin = async () => {
    const credentials = btoa(`${username}:${password}`);

    const response = await fetch(`http://127.0.0.1:8000/user/login`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        Authorization: `Basic ${credentials}`,
      },
    });

    if (response.ok) {
      localStorage.setItem('authToken', credentials);
      login();
      router.push('/');
    } else {
      alert('Login failed');
    }
  };

  const handleKeydown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4 text-center">Login</h1>
        <input
          type="text"
          placeholder="Username"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          onKeyDown={handleKeydown}
          className="border rounded-lg p-2 mb-4 w-full"
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          onKeyDown={handleKeydown}
          className="border rounded-lg p-2 mb-4 w-full"
        />
        <button
          onClick={handleLogin}
          className="px-4 py-2 bg-blue-500 text-white rounded-lg w-full hover:bg-blue-600 transition"
        >
          Login
        </button>
      </div>
    </div>
  );
}
