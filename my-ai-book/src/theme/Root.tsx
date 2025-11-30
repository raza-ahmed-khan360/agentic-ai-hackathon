import React from 'react';
import ChatWindow from '../components/ChatWindow';

// Default implementation, that you can customize
export default function Root({children}) {
  return (
    <>
      {children}
      <ChatWindow />
    </>
  );
}