import { Card, CardDescription, CardHeader, CardTitle } from '../components/ui/card';
import { FileText, Clock } from 'lucide-react';

const HistoryPage = () => {
  // Placeholder data
  const history = [
    { id: 1, name: 'Raport_Sprzedazy_Q1.pdf', date: '2023-10-24', status: 'Gotowy' },
    { id: 2, name: 'Analiza_Klientow.csv', date: '2023-10-23', status: 'Przetwarzanie' },
    { id: 3, name: 'Dane_Surowe_2023.xlsx', date: '2023-10-20', status: 'Błąd' },
  ];

  return (
    <div className="container mx-auto max-w-4xl p-6">
      <h1 className="mb-6 text-3xl font-bold tracking-tight">Historia Generowania</h1>

      <div className="grid gap-4">
        {history.map((item) => (
          <Card key={item.id} className="transition-shadow hover:shadow-md">
            <CardHeader className="flex flex-row items-center gap-4 py-4">
              <div className="rounded-full bg-secondary p-2">
                <FileText className="h-5 w-5 text-primary" />
              </div>
              <div className="flex-1">
                <CardTitle className="text-base">{item.name}</CardTitle>
                <CardDescription className="flex items-center gap-1 text-xs">
                  <Clock className="h-3 w-3" /> {item.date}
                </CardDescription>
              </div>
              <div className="text-sm font-medium">
                <span className={`rounded-full px-2 py-1 text-xs ${item.status === 'Gotowy' ? 'bg-green-100 text-green-700' :
                  item.status === 'Przetwarzanie' ? 'bg-blue-100 text-blue-700' :
                    'bg-red-100 text-red-700'
                  }`}>
                  {item.status}
                </span>
              </div>
            </CardHeader>
          </Card>
        ))}
      </div>
    </div>
  );
};

export default HistoryPage;
