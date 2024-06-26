"use client";
import LoadingScreenComponent from "@/components/loading-screens";
import { Button } from "@/components/ui/button";
import useResultStore from "@/stores/quiz-attempt-result";
import Link from "next/link";
import { useRouter } from "next/navigation";

export default function ResultPage() {
  const results = useResultStore((state) => state.results);
  const router = useRouter();
  // If Results are Null for 5 seconds, show error message
  if (!results) {
    setTimeout(() => {
      if (typeof window !== "undefined") {
        router.push("/dashboard");
      }
    }, 3000);

    return <LoadingScreenComponent />;
  }

  return (
    <>
      <QuizResultComponent
        attempt_score={results.attempt_score}
        total_points={results.total_points}
        time_finish={results.time_finish}
        time_start={results.time_start}
      />
    </>
  );
}

function QuizResultComponent({
  time_start,
  time_finish,
  attempt_score,
  total_points,
}: {
  time_start: string;
  time_finish: string;
  attempt_score: number;
  total_points: number;
}) {
  const { minutes, seconds } = calculateTimeTaken(time_start, time_finish);

  const percentage = calculatePercentage(attempt_score, total_points);

  return (
    <div className="flex space-y-4 flex-col items-center justify-center h-screen  bg-gradient-to-r from-custom-purple to-custom-blue">
      <Button className="my-5 text-sm" size={'lg'} variant={'outline'}>
        <Link
          className="flex items-center gap-2 text-sm font-semibold"
          href="/dashboard"
        >
          Go To Dashboard
        </Link>
      </Button>
      <div className="bg-white dark:bg-gray-800 rounded-lg shadow-md p-8 w-full max-w-md">
        <h1 className="text-2xl font-bold mb-4 p-3 text-center">
          Results
        </h1>
        <div className="grid grid-cols-2 gap-4">
          <div className="col-span-2 sm:col-span-1">
            <p className="text-gray-500 dark:text-gray-400 mb-1">
              Total Time Spent
            </p>
            <p className="font-medium">
              {minutes} minutes, {seconds} seconds
            </p>
          </div>
          <div className="col-span-2 sm:col-span-1">
            <p className="text-gray-500 dark:text-gray-400 mb-1">Score</p>
            <p className="font-medium">{percentage}%</p>
          </div>
          <div className="col-span-2">
            <p className="text-gray-500 dark:text-gray-400 mb-1">
              Total Points
            </p>
            <p className="font-medium">
              {attempt_score} / {total_points}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

const calculateTimeTaken = (time_start: string, time_finish: string) => {
  const startDate = new Date(time_start).getTime();
  const finishDate = new Date(time_finish).getTime();
  const timeDifference = finishDate - startDate; // Difference in milliseconds
  const minutes = Math.floor(timeDifference / 60000);
  const seconds = Math.floor((timeDifference % 60000) / 1000);
  return { minutes, seconds };
};

function calculatePercentage(attemptScore: any, totalScore: any) {
  const percentage = (attemptScore / totalScore) * 100;
  return (Math.round(percentage * 100) / 100).toFixed(2);
}
