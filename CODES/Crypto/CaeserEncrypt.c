#include<stdio.h>
#include<ctype.h>
int main(){
    char a[500],ch;
    int k;
    printf("Enter Any Text Max 500 letters:");
    scanf("%s",a);

    printf("Enter a Key for Encrypting:");
    scanf("%d",&k);

    for(int i=0;a[i]!='\0';i++){
        ch=a[i];
        if(ch){
            if(islower(ch)){
                ch=(ch-'a' +k)%26+'a';
            }
            if(isupper(ch)){
                ch=(ch-'A'+k)%26+'A';
            }
        }
        a[i]=ch;
    }
    printf("Encrypted Message is: %s",a);
    return 0;
}