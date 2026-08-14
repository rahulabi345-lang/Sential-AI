import { SkeletonBar } from './Skeleton';

export default function TableRowSkeleton() {
  return (
    <div className="grid grid-cols-[80px_1fr_140px_110px] items-center border-b border-border px-5 py-3 last:border-0">
      <SkeletonBar className="h-3 w-12" />
      <SkeletonBar className="h-3 w-2/3" />
      <SkeletonBar className="h-3 w-20" />
      <SkeletonBar className="ml-auto h-4 w-16" />
    </div>
  );
}