import { SkeletonBar } from './Skeleton';

export default function StatCardSkeleton() {
  return (
    <div className="rounded-lg border border-border bg-surface p-5 shadow-panel">
      <SkeletonBar className="mb-3 h-3 w-20" />
      <SkeletonBar className="mb-2 h-7 w-14" />
      <SkeletonBar className="h-3 w-28" />
    </div>
  );
}