import { Loader2 } from 'lucide-react';

import { Button } from '@/components/ui/button';

export function ButtonLoading() {
  return (
    <Button className="bg-red-600 w-full" disabled>
      <Loader2 className="mr-2 h-4 w-4 animate-spin bg-transparent" />
      Aguarde Enviando
    </Button>
  );
}
