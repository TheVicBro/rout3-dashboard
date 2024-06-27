import '../styles/globals.css';
import type { AppProps } from 'next/app';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { AuthProvider } from '../context/authContext';
import Layout from '../components/Layout';
import { useRouter } from 'next/router';

const queryClient = new QueryClient();

function MyApp({ Component, pageProps }: AppProps) {
  const router = useRouter();

  if (router.pathname === '/login') {
    // For login page, we do not use the layout
    return (
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <Component {...pageProps} />
        </AuthProvider>
      </QueryClientProvider>
    );
  }

  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <Layout>
          <Component {...pageProps} />
        </Layout>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default MyApp;
