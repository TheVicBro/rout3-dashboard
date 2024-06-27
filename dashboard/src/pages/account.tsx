import { useEffect } from 'react';
import { useRouter } from 'next/router';
import Account from '../components/Account';
import { useAuth } from '../context/authContext';

export default function AccountPage() {
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

  return <Account />;
}
