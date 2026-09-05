import type { Metadata } from 'next';
import './globals.css';
import { Navbar } from '@/components/Navbar';
import { Sidebar } from '@/components/Sidebar';
import { ProjectProvider } from '@/hooks/useProject';

export const metadata: Metadata = {
  title: 'Data Centre EPC | AI Intelligence Platform',
  description: 'AI intelligence layer over Data Centre Engineering, Procurement, Construction, and Commissioning Delivery.',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body className="min-h-screen bg-slate-950 text-slate-100 antialiased font-sans flex flex-col selection:bg-cyan-500/30 selection:text-cyan-200">
        <ProjectProvider>
          <Navbar />
          <div className="flex flex-1 overflow-hidden">
            <Sidebar />
            <main className="flex-1 overflow-y-auto p-4 sm:p-6 lg:p-8 custom-scrollbar">
              <div className="max-w-7xl mx-auto space-y-6">
                {children}
              </div>
            </main>
          </div>
        </ProjectProvider>
      </body>
    </html>
  );
}
