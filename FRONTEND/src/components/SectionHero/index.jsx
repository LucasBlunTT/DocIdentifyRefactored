'use client';

import React, { useEffect, useState } from 'react';
import Container from '../Container';
import { Input } from '../ui/input';
import InputFile from '../InputFile';
import { Button } from '../ui/button';
import { ButtonLoading } from '../ui/buttonLoading';
import Help from '@/components/Help';

export default function SectionHero() {
  const [documento, setDocumento] = useState(null);
  const [nome, setNome] = useState('');
  const [cpf, setCpf] = useState('');
  const [dataNascimento, setDataNascimento] = useState('');
  const [dataVencimento, setDataVencimento] = useState('');
  const [loading, setLoading] = useState(false);

  async function handlerEnviarImagem(event) {
    event.preventDefault();
    const formData = new FormData();
    formData.append('image', documento[0]);
    try {
      setLoading(true);
      const URL = 'http://127.0.0.1:5000/upload';
      const response = await fetch(URL, {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const responseData = await response.json();
        console.log(responseData);
        const { nome, cpf, nascimento, dtVencimentoCnh } = responseData;
        setNome(nome);
        setCpf(cpf);
        setDataVencimento(dtVencimentoCnh);
      }
    } catch (error) {
      setLoading(false);
      throw new Error(error.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="w-full h-screen flex items-center justify-center">
      <Container className="relative">
        <form
          className="flex-col items-center justify-center"
          onSubmit={handlerEnviarImagem}
        >
          <div className="grid grid-cols-2 gap-10 mb-12">
            <Input
              type="text"
              id="nome"
              value={nome}
              onChange={(event) => setNome(event.target.value)}
              nomeLabel="Nome"
              placeholder="Nome"
            />
            <Input
              type="text"
              id="cpf"
              value={cpf}
              onChange={(event) => setCpf(event.target.value)}
              nomeLabel="CPF"
              placeholder="___.___.___-__"
            />
            <Input
              type="text"
              id="birthdate"
              value={dataNascimento}
              onChange={(event) => setDataNascimento(event.target.value)}
              nomeLabel="Data de Nascimento"
              placeholder="__/__/____"
            />
            <Input
              type="text"
              id="dataVenc"
              value={dataVencimento}
              onChange={(event) => setDataVencimento(event.target.value)}
              nomeLabel="Data de Vencimento"
              placeholder="__/__/____"
            />
          </div>
          <div
            className={`relative mb-4 cursor-pointer w-full h-[200px] border-[4px] border-dashed ${
              documento ? 'border-[green]' : 'border-[#FBF9FE]'
            } flex items-center justify-center`}
          >
            <p className="text-[#FBF9FE] text-xl absolute z-1">
              {documento ? documento[0].name : 'CLIQUE EM MIM 😍'}
            </p>
            <InputFile
              type="file"
              onChange={(event) => setDocumento(event.target.files)}
              className={'cursor-pointer'}
              accept=".png, .jpg, .jpeg"
            />
          </div>
          {loading ? (
            <ButtonLoading>Enviando</ButtonLoading>
          ) : (
            <Button>Enviar</Button>
          )}
        </form>
        <Help />
      </Container>
    </section>
  );
}
