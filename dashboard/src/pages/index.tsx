import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Secrets from '../components/Secrets';
import { useAuth } from '../context/authContext';

export default function Home() {
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

  return <Secrets />;
}
