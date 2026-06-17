import QRCode from 'qrcode';

const target = process.env.QR_URL || 'http://localhost:4200/cardapiodigital';

await QRCode.toFile(
  'public/assets/qr/qr-cardapio-digital.png',
  target,
  {
    errorCorrectionLevel: 'H',
    margin: 1,
    width: 512,
    color: {
      dark: '#02142C',
      light: '#FFFDF8',
    },
  }
);

console.log('QR Code gerado para:', target);
