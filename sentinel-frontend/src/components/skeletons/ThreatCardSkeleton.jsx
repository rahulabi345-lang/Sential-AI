import { SkeletonBar } from './Skeleton';

export default function ThreatCardSkeleton() {
  return (
    <div className="rounded-lg border border-border bg-surface p-4 shadow-panel">
      <SkeletonBar className="mb-3 h-3 w-16" />
      <SkeletonBar className="mb-2 h-4 w-3/4" />
      <SkeletonBar className="mb-1 h-3 w-full" />
      <SkeletonBar className="mb-4 h-3 w-2/3" />
      <SkeletonBar className="h-8 w-full" />
    </div>
  );
}