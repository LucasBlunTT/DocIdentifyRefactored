import Image from 'next/image';
import React from 'react';
import escIcon from '../../assets/icons8-esc-50.png';

function Help() {
  return (
    <ul className="absolute left-[-357px] flex items-center justify-center">
      <li className="flex items-center justify-center">
        <Image className="mr-2" src={escIcon} alt="esc icon" />
        <p>PARA LIMPAR TUDO</p>
      </li>
    </ul>
  );
}

export default Help;
