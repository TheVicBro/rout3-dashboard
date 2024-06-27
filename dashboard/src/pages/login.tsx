import { useState } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '../context/authContext';

export default function Login() {
  const { login } = useAuth();
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isRegistering, setIsRegistering] = useState(false);
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

  const handleRegister = async () => {
    if (password !== confirmPassword) {
      alert('Passwords do not match');
      return;
    }

    const response = await fetch(`http://127.0.0.1:8000/user/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        username,
        password,
      }),
    });

    if (response.ok) {
      alert('Registration successful');
      setIsRegistering(false);
    } else {
      alert('Registration failed');
    }
  };

  const handleKeydown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      isRegistering ? handleRegister() : handleLogin();
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
        <h1 className="text-3xl font-bold mb-4 text-center">{isRegistering ? 'Register' : 'Login'}</h1>
        {isRegistering ? (
          <>
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
            <input
              type="password"
              placeholder="Confirm Password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              onKeyDown={handleKeydown}
              className="border rounded-lg p-2 mb-4 w-full"
            />
            <button
              onClick={handleRegister}
              className="px-4 py-2 bg-blue-500 text-white rounded-lg w-full hover:bg-blue-600 transition"
            >
              Register
            </button>
            <p className="mt-4 text-center text-gray-600">
              Already have an account?{' '}
              <span
                className="text-blue-500 cursor-pointer"
                onClick={() => setIsRegistering(false)}
              >
                Login
              </span>
            </p>
          </>
        ) : (
          <>
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
            <p className="mt-4 text-center text-gray-600">
              Don't have an account?{' '}
              <span
                className="text-blue-500 cursor-pointer"
                onClick={() => setIsRegistering(true)}
              >
                Register
              </span>
            </p>
          </>
        )}
      </div>
    </div>
  );
}
