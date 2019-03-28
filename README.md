# password-manager
Python script for managing your usernames and passwords.

## Usage

When the script is executed, the user must enter a password first. This password will be used to encrypt and decrypt all usernames and passwords. There is no check if this key is correct or not. If it is incorrect, decryption will give wrong results. 

```
Enter cryption key: >> *Enter your key here*
```

Once this key is initialized, there are some commands you can run to start managing your passwords.

```
>> add
```
This command will ask you the platform and your username for that platform and create a random password for it for you to set. It will automatically encrypt and save it.

```
>> hard
```
This command will ask you the platform, your username for that platform and your password. This method won't generate a random password and ask you to write one. It will automatically encrypt and save it.

```
>> get (who)
```
This command will return your username and password. You can write the platform as an argument. It will also work without arguments.

```
>> delete (who)
```
This command will delete your username and password. You can write the platform as an argument. It will also work without arguments.

```
>> search (key)
```
This command will search the given key through platforms. Key even may be even a character. You can write the key as an argument. It will also work without arguments.

```
>> change (who) (flag) (newValue)
```
This command will change existing values. First argument is the platform, second argument is user or pass flag and third argument is the new value. It will also work without arguments. If the flag is pass and the value is "random", a random password will be generated.

```
>> all
```
This command will list all your data.

```
>> exit
```
This command will finish the application. Please note that the content on the clipboard stays.


## License

This project has been created for fun and self usage. Anyone can download and use.