import Image from "next/image";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-6 bg-transparent">
      <div className="z-10 w-full max-w-lg mb-12 text-center">
        <h1 className="text-5xl font-extrabold tracking-tight text-gray-900 sm:text-6xl mb-4">
          Evolution of <span className="text-blue-600">Todo</span>
        </h1>
        <p className="text-lg text-gray-500 font-medium tracking-wide uppercase">Phase II</p>
      </div>

      <div className="bg-white/80 backdrop-blur-sm border border-gray-100 p-10 rounded-2xl shadow-xl w-full max-w-md">
        <h2 className="text-3xl font-bold mb-2 text-gray-900 text-center">Welcome</h2>
        <p className="text-gray-500 mb-10 text-center leading-relaxed">
          Persistent, Multi-user Todo Management for modern workflows.
        </p>

        <div className="flex flex-col gap-4">
          <a
            href="/auth/signin"
            className="group relative flex justify-center py-3 px-4 border border-transparent text-sm font-semibold rounded-xl text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 shadow-lg shadow-blue-200"
          >
            Sign In
          </a>
          <a
            href="/auth/signup"
            className="flex justify-center py-3 px-4 border-2 border-gray-100 text-sm font-semibold rounded-xl text-gray-700 bg-white hover:bg-gray-50 hover:border-blue-100 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200"
          >
            Create Account
          </a>
        </div>
      </div>

      <footer className="mt-20 text-gray-400 text-sm">
        &copy; 2026 Evolution of Todo. All rights reserved.
      </footer>
    </main>
  );
}
