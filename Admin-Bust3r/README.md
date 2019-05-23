# Admin-Bust3r

A powerful, fast and advanced admin panel finder(buster) tool in python3. 

### Installing

```
git clone https://github.com/be1iev3r/Admin-Bust3r.git
```

### Prerequisites

* python3

### Usage

* Help

```
python3 admin-bust3r.py --help
```

* Example

```
python3 admin-bust3r.py -u http://example.com
```

* For specific extension only. Ex: [php, asp, htlm, aspx]

```
python3 admin-bust3r.py -u http://example.com -e php
```

* For other wordlists (default=medium). Ex: [small, large, verylarge]

```
python3 admin-bust3r.py -u http://example.com -s
python3 admin-bust3r.py -u http://example.com -l
python3 admin-bust3r.py -u http://example.com -vl
```

* For Fast scan mode.

```
python3 admin-bust3r.py -u http://example.com -f
```

* To save result in output file

```
python3 admin-bust3r.py -u http://example.com -o <outfile>
```
