
"use client";

import { useEffect, useState } from "react";

// FastAPI에서 반환하는 응답 형식
interface HealthResponse {
  status: string;
  message: string;
}

export default function Home() {
  // API 연결 상태 관리
  const [status, setStatus] = useState("연결 확인 중...");
  const [message, setMessage] = useState("");

  useEffect(() => {
    // FastAPI 서버에 요청
    async function checkBackend() {
      try {
        const response = await fetch(
          "http://127.0.0.1:8000/api/health"
        );

        if (!response.ok) {
          throw new Error("API 요청 실패");
        }

        const data: HealthResponse = await response.json();

        // 서버 응답 확인
        if (data.status === "ok") {
          setStatus("연결 성공");
          setMessage(data.message);
        } else {
          setStatus("서버 상태 확인 필요");
        }
      } catch (error) {
        setStatus("연결 실패");
        setMessage("FastAPI 서버 실행 상태를 확인하세요.");
        console.error(error);
      }
    }

    checkBackend();
  }, []);

  return (
    <main className="flex min-h-screen flex-col items-center justify-center gap-6 bg-zinc-950 text-white">
      <h1 className="text-4xl font-bold">
        FFXIV Damage Simulator
      </h1>

      <p className="text-zinc-400">
        파이널판타지14 기대 피해량 계산기
      </p>

      <div className="rounded-xl border border-zinc-700 bg-zinc-900 p-6 text-center">
        <h2 className="mb-3 text-xl font-semibold">
          FastAPI 연결 상태
        </h2>

        <p className="text-lg">{status}</p>
        <p className="mt-2 text-sm text-zinc-400">
          {message}
        </p>
      </div>
    </main>
  );
}
