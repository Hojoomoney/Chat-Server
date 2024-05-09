'use client'
import Image from "next/image";
import { useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";

export default function Home() {
  const [message, setMessage] = useState('')
  
  type Inputs = {
    question: string
    exampleRequired?: string
  }
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()
  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log('입력된 값' + JSON.stringify(data))
    fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then((response) => response.json())
    .then((data) => {
      setMessage(data.answer);
    })
    .catch((error) => console.log("error:", error));
  }

  console.log(watch("question"));

  return (
    <>
      <div className="h-[80vh] items-center flex justify-center px-5 lg:px-0">
        <div className="flex flex-col items-center justify-center w-full text-2xl xl:text-4xl font-extrabold text-900">
          <h1> How can I help you today? </h1>
        </div></div>
      <div className="mx-auto w-[1000px] flex flex-col gap-4">
      <form onSubmit={handleSubmit(onSubmit)}>
        {<h4 className="text-center">{message? message : ""}</h4>}
        <input {...register("question", { required: true })}
          className="w-full px-5 py-3 rounded-lg font-medium bg-gray-100 border border-gray-200 placeholder-gray-500 text-sm focus:outline-none focus:border-gray-400 focus:bg-white"
          type="text"
          placeholder="Send Message"
        />
        <button type="submit" className="w-full h-[40px] relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-lg group bg-gradient-to-br from-pink-500 to-orange-400 group-hover:from-pink-500 group-hover:to-orange-400 hover:text-white dark:text-white focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800">Send</button>
      {errors.question && <span>This field is required</span>}
      </form>
      </div>
    </>
  );
}
