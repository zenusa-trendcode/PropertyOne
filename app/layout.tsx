import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: 'PropertiOne PMS',
  description:
    'Dashboard property management untuk okupansi, tenant, lease, billing, maintenance, inspeksi, dan risiko operasional.',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="id">
      <body>{children}</body>
    </html>
  );
}
