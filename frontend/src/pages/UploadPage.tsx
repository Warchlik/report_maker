import React, { useState, useRef, useCallback } from 'react';
import { UploadCloud, File as FileIcon, X, CheckCircle, AlertCircle } from 'lucide-react';
import { Button } from '../components/ui/button';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';

type UploadStatus = 'idle' | 'loading' | 'success' | 'error';

const UploadPage = () => {
  const [file, setFile] = useState<File | null>(null);
  const [status, setStatus] = useState<UploadStatus>('idle');
  const [message, setMessage] = useState<string>('');
  const fileInputRef = useRef<HTMLInputElement>(null);

  // Format file size
  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setFile(e.target.files[0]);
      setStatus('idle');
      setMessage('');
    }
  };

  const handleDragOver = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
      setStatus('idle');
      setMessage('');
    }
  }, []);

  const removeFile = () => {
    setFile(null);
    setStatus('idle');
    setMessage('');
    if (fileInputRef.current) fileInputRef.current.value = '';
  };

  const handleGenerateReport = async () => {
    if (!file) return;

    setStatus('loading');
    setMessage('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      // TODO: Prawdziwy endpoint backendu
      // W przyszłości zamień URL na zmienną środowiskową np. import.meta.env.VITE_API_URL
      const response = await fetch('http://localhost:8080/api/report', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error(`Błąd serwera: ${response.status}`);
      }

      // TODO: Obsługa odpowiedzi JSON, np. const data = await response.json();

      setStatus('success');
      setMessage('Raport jest generowany. Otrzymasz powiadomienie po zakończeniu.');
    } catch (error) {
      console.error('Upload failed:', error);
      setStatus('error');
      setMessage(error instanceof Error ? error.message : 'Wystąpił nieoczekiwany błąd podczas przesyłania.');
    }
  };

  return (
    <div className="flex h-full w-full items-center justify-center p-6">
      <Card className="w-full max-w-2xl">
        <CardHeader>
          <CardTitle>Generator Raportów</CardTitle>
          <CardDescription>
            Prześlij plik z danymi, aby wygenerować szczegółowy raport analityczny.
          </CardDescription>
        </CardHeader>
        <CardContent>

          {/* Drag & Drop Area */}
          {!file && (
            <div
              onDragOver={handleDragOver}
              onDrop={handleDrop}
              className="group relative flex h-64 w-full cursor-pointer flex-col items-center justify-center rounded-lg border-2 border-dashed border-muted-foreground/25 bg-muted/50 transition-colors hover:bg-muted"
              onClick={() => fileInputRef.current?.click()}
            >
              <div className="flex flex-col items-center justify-center space-y-4 px-4 text-center">
                <div className="rounded-full bg-background p-4 shadow-sm ring-1 ring-input transition-all group-hover:scale-110">
                  <UploadCloud className="h-8 w-8 text-muted-foreground" />
                </div>
                <div className="space-y-1">
                  <p className="text-sm font-medium text-muted-foreground">
                    <span className="font-semibold text-primary">Kliknij, aby wybrać</span> lub przeciągnij plik tutaj
                  </p>
                  <p className="text-xs text-muted-foreground/70">
                    CSV, Excel, PDF (max. 10MB)
                  </p>
                </div>
              </div>
              <input
                ref={fileInputRef}
                type="file"
                className="hidden"
                onChange={handleFileSelect}
              />
            </div>
          )}

          {/* Selected File View */}
          {file && (
            <div className="relative flex items-center gap-4 rounded-lg border bg-card p-4 shadow-sm">
              <div className="rounded-full bg-primary/10 p-2">
                <FileIcon className="h-6 w-6 text-primary" />
              </div>
              <div className="flex-1 space-y-1">
                <p className="text-sm font-medium leading-none">{file.name}</p>
                <p className="text-xs text-muted-foreground">
                  {formatFileSize(file.size)} • {file.type || 'Nieznany typ'}
                </p>
              </div>
              <Button
                variant="ghost"
                size="icon"
                className="h-8 w-8 text-muted-foreground hover:text-destructive"
                onClick={removeFile}
                disabled={status === 'loading'}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          )}

          {/* Status Messages */}
          {status === 'success' && (
            <div className="mt-4 flex items-center gap-2 rounded-md bg-green-50 p-3 text-sm text-green-700">
              <CheckCircle className="h-4 w-4" />
              <span>{message}</span>
            </div>
          )}
          {status === 'error' && (
            <div className="mt-4 flex items-center gap-2 rounded-md bg-red-50 p-3 text-sm text-red-700">
              <AlertCircle className="h-4 w-4" />
              <span>{message}</span>
            </div>
          )}

        </CardContent>
        <CardFooter className="flex justify-between">
          <Button variant="outline" onClick={removeFile} disabled={!file || status === 'loading'}>
            Anuluj
          </Button>
          <Button
            onClick={handleGenerateReport}
            disabled={!file || status === 'loading'}
          >
            {status === 'loading' ? 'Przetwarzanie...' : 'Wygeneruj raport'}
          </Button>
        </CardFooter>
      </Card>
    </div>
  );
};

export default UploadPage;
