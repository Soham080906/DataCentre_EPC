import React from 'react';
import { cn } from '@/lib/utils';

interface CardProps extends React.HTMLAttributes<HTMLDivElement> {
  children: React.ReactNode;
  className?: string;
  glow?: boolean;
}

export const Card: React.FC<CardProps> = ({ children, className, glow = false, ...props }) => {
  return (
    <div
      className={cn(
        'relative rounded-xl bg-slate-900/60 border border-slate-800/80 p-5 backdrop-blur-md transition-all duration-200 hover:border-slate-700/80',
        glow && 'before:absolute before:-inset-px before:rounded-xl before:bg-gradient-to-r before:from-cyan-500/20 before:to-blue-500/20 before:-z-10',
        className
      )}
      {...props}
    >
      {children}
    </div>
  );
};
