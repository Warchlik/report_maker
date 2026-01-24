import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '../components/ui/card';

const RegisterPage = () => {
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Rejestracja placeholder...");
    // TODO: Implementacja rejestracji
  };

  return (
    <div className="flex h-full w-full items-center justify-center p-6">
      <Card className="w-full max-w-sm">
        <CardHeader>
          <CardTitle className="text-2xl">Rejestracja</CardTitle>
          <CardDescription>
            Utwórz nowe konto, aby rozpocząć korzystanie z serwisu.
          </CardDescription>
        </CardHeader>
        <form onSubmit={handleSubmit}>
          <CardContent className="grid gap-4">
            <div className="grid gap-2">
              <Label htmlFor="full-name">Imię i Nazwisko</Label>
              <Input id="full-name" placeholder="Jan Kowalski" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="email">Email</Label>
              <Input id="email" type="email" placeholder="m@example.com" required />
            </div>
            <div className="grid gap-2">
              <Label htmlFor="password">Hasło</Label>
              <Input id="password" type="password" required />
            </div>
          </CardContent>
          <CardFooter className="flex flex-col gap-4">
            <Button className="w-full" type="submit">Utwórz konto</Button>
            <div className="text-center text-sm text-muted-foreground">
              Masz już konto?{" "}
              <Link to="/login" className="underline hover:text-primary">
                Zaloguj się
              </Link>
            </div>
          </CardFooter>
        </form>
      </Card>
    </div>
  );
};

export default RegisterPage;
