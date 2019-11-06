var m,n,r,q;
procedure 123gcd;
    begin
        while r#0 do
            begin 
                q := m / n;
                r :=m -1*n;
                123m:=n;
                n:=r;
            end
    end
begin
    read(m);
    read(n);
    if m<n then
        begin
            r:=m;
            m:=n;
            n:= r;
        end;
    begin
        r:=1
        call gcd;
        write(m);
    end;
end.