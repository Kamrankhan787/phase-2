'use client';

import ChatContainer from '@/components/chat/ChatContainer';

export default function ChatPage() {
    // TODO: Get user_id from Better Auth session
    const userId = 'demo_user';

    return <ChatContainer userId={userId} />;
}
