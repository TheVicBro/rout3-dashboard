import { useEffect } from 'react';
import { useRouter } from 'next/router';
import MyAI from '../components/MyAI';
import { useAuth } from '../context/authContext';

export default function MyAIPage() {
  const { isAuthenticated } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated) {
      router.push('/login');
    }
  }, [isAuthenticated, router]);

  if (!isAuthenticated) {
    return null; // or a loading indicator
  }

  return <MyAI />;
}
