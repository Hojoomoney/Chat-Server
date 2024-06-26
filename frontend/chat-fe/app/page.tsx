'use client'
import Image from "next/image";
import { useState } from "react";
import { SubmitHandler, useForm } from "react-hook-form";

export default function Home() {
  const [message, setMessage] = useState('')

  type Inputs = {
    question: string
    exampleRequired?: string
    category: string
  }
  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<Inputs>()
  const onSubmit: SubmitHandler<Inputs> = (data) => {
    console.log('입력된 값' + JSON.stringify(data))
    fetch('http://localhost:8000/api/chat/' + data.category, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => response.json()) // Add 'return' before response.json()
      .then((data) => {
        console.log('응답' + JSON.stringify(data));
        console.log(data.answer);
        setMessage(data.answer);
      })
      .catch((error) => console.log("error:", error));
  }

  console.log(watch("question"));

  return (
    <>
 <div className="bg-cover h-[100vh] flex flex-col items-center justify-center px-5 lg:px-0" style={{ backgroundImage: "url('https://cdn.pixabay.com/photo/2015/11/06/11/52/question-mark-1026531_1280.jpg')",backgroundSize: "100% 100%", backdropFilter: "blur(30px)", }}>
  <h1 className="text-3xl xl:text-4xl font-bold text-black" style={{marginTop: "300px", marginBottom: "70px"}}><span style={{ fontSize: "50px" }}>무엇이든 물어보세요!</span></h1>
  <div className="flex flex-col gap-4 mt-10 mb-10" style={{marginTop: "200px", marginBottom: "50px"}}>
    <form onSubmit={handleSubmit(onSubmit)}>

    {message ?  <input className="text-center w-[1200px] h-[80px] px-5 py-3 rounded-lg font-bold bg-white border border-black" style={{ fontSize: 24,marginTop: "-70px",marginBottom:"50px", color:"black"}} value={message}/>  : ""}
    <div className="text-center">
        <input {...register("category")} type="radio" value="titanic" style={{ width: "20px", height: "20px" }} defaultChecked /> <span style={{ color: "black", fontSize: "24px" }}>Titanic</span>
        <input {...register("category")} type="radio" value="capital" style={{ width: "20px", height: "20px" }} /> <span style={{ color: "black", fontSize: "24px" }}>Capital</span>
        <input {...register("category")} type="radio" value="other" style={{ width: "20px", height: "20px" }} /> <span style={{ color: "black", fontSize: "24px" }}>Other</span>
        </div>
        <br />
      <input
        {...register("question", { required: true })}
        className="w-[1200px] h-[60px] px-5 py-3 rounded-lg font-bold bg-transparent border border-black placeholder-black text-sm focus:outline-none focus:border-gray-400 focus:bg-white"
        type="text"
        placeholder="원하는 질문을 입력해주세요."
        style={{ fontSize: 20 }}
      />
      <button
        type="submit"
        className="w-[150px] h-[60px] rounded-lg bg-pink-500 text-white font-medium hover:bg-pink-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-pink-500"
      >
        Send
      </button>
    </form>
  </div>
</div>
    </>
  );
}
