import { FileInput } from "@/components/FileInput";



export default function Upload() {
  return (
    <>
      <div className="flex flex-row h-full w-full items-center justify-center p-8">
        <div className="w-full max-w-2xl">
          <FileInput />
        </div>
      </div>
    </>
  )
} 
