class GeneralValidator {
  static validateEmail(email: string): boolean {
    const expression: RegExp = /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return expression.test(email);
  }

  static validateCpf(value: string) {
    if (typeof value !== 'string') {
      return false;
    }

    value = value.replace(/[^\d]+/g, '');

    if (value.length !== 11 || !!value.match(/(\d)\1{10}/)) {
      return false;
    }

    const values = value.split('').map(el => +el);
    const rest = (count: number) => (values.slice(0, count - 12).reduce((soma, el, index) => (soma + el * (count - index)), 0) * 10) % 11 % 10;

    return rest(10) === values[9] && rest(11) === values[10];
  }

  static validateCnpj(cnpj: string): boolean {
    // Remove any non-digit characters
    cnpj = cnpj.replace(/[^\d]/g, '');

    // CNPJ must have 14 digits
    if (cnpj.length !== 14) {
      return false;
    }

    // Validate the first check digit
    let sum = 0;
    let weight = 5;
    for (let i = 0; i < 12; i++) {
      sum += parseInt(cnpj[i]) * weight;
      weight = (weight === 2) ? 9 : weight - 1;
    }
    let digit = (sum % 11 < 2) ? 0 : 11 - (sum % 11);
    if (parseInt(cnpj[12]) !== digit) {
      return false;
    }

    // Validate the second check digit
    sum = 0;
    weight = 6;
    for (let i = 0; i < 13; i++) {
      sum += parseInt(cnpj[i]) * weight;
      weight = (weight === 2) ? 9 : weight - 1;
    }
    digit = (sum % 11 < 2) ? 0 : 11 - (sum % 11);
    if (parseInt(cnpj[13]) !== digit) {
      return false;
    }

    return true;
  }
}

export default GeneralValidator;