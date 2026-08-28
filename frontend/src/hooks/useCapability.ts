import { useQuery } from '@tanstack/react-query';
import { getCapability } from '../api/capability';

export function useCapability() {
  return useQuery({
    queryKey: ['capability'],
    queryFn: getCapability,
  });
}
