import { useDropzone } from "react-dropzone"
import { Upload } from "lucide-react"
import { cn } from "@/lib/utils"
import { useCallback } from "react"

export function FileInput() {
  const onDrop = useCallback((acceptedFiles: File[]) => {
    console.log("Pliki do wysłania:", acceptedFiles)
  }, [])

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.ms-excel': ['.xls'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/json': ['.json']
    }
  })

  // return (
  //   <Card
  //     {...getRootProps()}
  //     className={cn(
  //       "cursor-pointer border-dashed transition-colors duration-200",
  //       // NOWE: Minimalna wysokość 400px i flex, żeby wszystko było na środku
  //       "min-h-[400px] w-full flex items-center justify-center",
  //       isDragActive ? "border-primary bg-primary/5" : "hover:bg-muted/50"
  //     )}
  //   >
  //     <CardContent className="flex flex-col items-center justify-center space-y-4 px-6 py-12">
  //       <input {...getInputProps()} />
  //
  //       {/* Lekko powiększona ikona w okręgu, żeby lepiej pasowała do dużej karty */}
  //       <div className="flex h-16 w-16 items-center justify-center rounded-full border border-dashed border-muted-foreground/50 bg-background">
  //         <Upload className="h-8 w-8 text-muted-foreground" />
  //       </div>
  //
  //       <div className="text-center space-y-2">
  //         {/* Nieco większy tekst główny */}
  //         <p className="text-lg font-medium">
  //           <span className="text-primary font-semibold">Click to upload</span> or drag and drop
  //         </p>
  //         <p className="text-sm text-muted-foreground">
  //           CSV, XLS, XLSX, JSON (max. 10MB)
  //         </p>
  //       </div>
  //     </CardContent>
  //   </Card>
  // )

  return (
    <div
      {...getRootProps()}
      className={cn(
        "relative flex w-full flex-col items-center justify-center rounded-xl border-2 border-dashed border-muted-foreground/25 transition-all hover:bg-muted/25",
        "h-64 px-6 py-4",
        isDragActive ? "border-primary/50 bg-primary/5 scale-[1.01]" : "bg-background",
        "cursor-pointer"
      )}
    >
      <input {...getInputProps()} />

      <div className="flex flex-col items-center gap-4 text-center">
        <div className="flex h-14 w-14 items-center justify-center rounded-full bg-muted/50 shadow-sm ring-1 ring-inset ring-muted-foreground/10">
          <Upload className="h-7 w-7 text-muted-foreground" aria-hidden="true" />
        </div>

        <div className="space-y-1">
          <p className="text-base font-medium text-foreground">
            <span className="text-primary font-semibold hover:underline">Click to upload</span> or drag and drop
          </p>
          <p className="text-sm text-muted-foreground">
            CSV, XLS, XLSX, JSON (max. 10MB)
          </p>
        </div>
      </div>
    </div>
  )
}
