import { SkeletonBar } from './Skeleton';

export default function ChartSkeleton({ height = 'h-56' }) {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <SkeletonBar className="mb-1 h-3 w-32" />
      <SkeletonBar className="mb-4 h-3 w-48" />
      <SkeletonBar className={`${height} w-full`} />
    </div>
  );
}