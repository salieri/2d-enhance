from config import Config

(a, err) = Config.Schema().load(
    {
        "processor": {
            "native": {
                "size" : {
                    "width": 101,
                    "height": 102
                }
            }
        },

        "output": {
            "targets": [
                {
                    "name": "prediction"
                }
            ]
        },

        "content": {
            "grid": {
                "size": {
                }
            },

            "types": [
                {
                    "type": "sprite",
                    "chance": 0.3
                }
            ]
        }


    }
)

print('Moooo')
print(err)
print(a)

print(a.output)