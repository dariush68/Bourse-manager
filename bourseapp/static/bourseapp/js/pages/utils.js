function toJalaliDate(date) {
    const d = new Date(date);
    let options = { year: 'numeric', month: 'numeric', day: 'numeric', };
    const datec2 = new Intl.DateTimeFormat('fa-IR', options).format(d);
    return datec2;
}